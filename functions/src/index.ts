import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

admin.initializeApp();

const db = admin.firestore();

/**
 * Triggered when a match result is updated.
 * Validates predictions and awards XP server-side.
 */
export const onMatchResultUpdate = functions.firestore
  .document('matches/{matchId}')
  .onUpdate(async (change, context) => {
    const newData = change.after.data();
    const oldData = change.before.data();

    // Only run if status changed to 'completed'
    if (newData.status !== 'completed' || oldData.status === 'completed') {
      return null;
    }

    const { matchId } = context.params;
    const result = newData.result; // { winner, topScorer, topBowler, score }

    // Fetch all predictions for this match
    const predictionsSnapshot = await db.collection('predictions')
      .where('matchId', '==', matchId)
      .where('status', '==', 'pending')
      .get();

    const batch = db.batch();

    predictionsSnapshot.forEach((doc) => {
      const pred = doc.data();
      let earnedXP = 0;

      // 1. Match Winner (+100)
      if (pred.winner === result.winner) earnedXP += 100;

      // 2. Top Scorer (+250)
      if (pred.topScorer === result.topScorer) earnedXP += 250;

      // 3. Top Bowler (+250)
      if (pred.topBowler === result.topBowler) earnedXP += 250;

      // 4. Score Range (+150 / +50)
      const diff = Math.abs(pred.predictedScore - result.score);
      if (diff === 0) earnedXP += 150;
      else if (diff <= 10) earnedXP += 50;

      // Update User XP
      const userRef = db.collection('users').doc(pred.userId);
      batch.update(userRef, {
        xp: admin.firestore.FieldValue.increment(earnedXP),
        lastProcessedMatch: matchId
      });

      // Mark prediction as processed
      batch.update(doc.ref, { status: 'processed', awardedXP: earnedXP });
    });

    return batch.commit();
  });

/**
 * Broadcast FCM notification to all users.
 */
export const sendBroadcastNotification = functions.https.onCall(async (data, context) => {
  // Check for admin custom claim
  if (!context.auth?.token.admin) {
    throw new functions.https.HttpsError('permission-denied', 'Only admins can broadcast.');
  }

  const { title, body } = data;

  const message = {
    notification: { title, body },
    topic: 'all_users'
  };

  return admin.messaging().send(message);
});

/**
 * Daily Streak Reset @ Midnight IST (Triggered via Pub/Sub)
 */
export const resetStreaks = functions.pubsub
  .schedule('0 0 * * *')
  .timeZone('Asia/Kolkata')
  .onRun(async () => {
    const now = admin.firestore.Timestamp.now();
    const twentyFourHoursAgo = new Date(now.toDate().getTime() - 24 * 60 * 60 * 1000);

    const inactiveUsers = await db.collection('users')
      .where('lastActive', '<', twentyFourHoursAgo)
      .get();

    const batch = db.batch();
    inactiveUsers.forEach(doc => {
      batch.update(doc.ref, { streak: 0 });
    });

    return batch.commit();
  });
