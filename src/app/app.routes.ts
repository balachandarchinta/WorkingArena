import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard';
import { PredictComponent } from './components/predict/predict';
import { FantasyComponent } from './components/fantasy/fantasy';
import { LeaderboardComponent } from './components/leaderboard/leaderboard';
import { XpComponent } from './components/xp/xp';
import { AiCoachComponent } from './components/ai-coach/ai-coach';
import { AdminComponent } from './components/admin/admin';
import { DocsComponent } from './components/docs/docs';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'predict', component: PredictComponent },
  { path: 'fantasy', component: FantasyComponent },
  { path: 'leaderboard', component: LeaderboardComponent },
  { path: 'xp', component: XpComponent },
  { path: 'ai-coach', component: AiCoachComponent },
  { path: 'admin', component: AdminComponent },
  { path: 'docs', component: DocsComponent },
];
