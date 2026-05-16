import { Component, EventEmitter, Output, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { gsap } from 'gsap';

@Component({
  selector: 'app-mascot-intro',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mascot-intro.html',
  styleUrl: './mascot-intro.css'
})
export class MascotIntroComponent implements AfterViewInit {
  @Output() dismissed = new EventEmitter<void>();
  @ViewChild('ball') ball!: ElementRef;
  @ViewChild('rings') rings!: ElementRef;

  rules = [
    { title: 'Predict Winner', desc: 'Pick the match winner and earn 100 XP.' },
    { title: 'Top Scorer', desc: 'Identify the highest run-getter for 250 XP.' },
    { title: 'Top Bowler', desc: 'Spot the leading wicket-taker for 250 XP.' },
    { title: 'Score Range', desc: 'Guess the total score within 10 runs.' },
    { title: 'Build Fantasy', desc: 'Assemble your 11 within a 100-credit budget.' },
    { title: 'Multipliers', desc: 'Boost points with Captain (2x) and Vice-Captain (1.5x).' }
  ];

  ngAfterViewInit() {
    this.animateMascot();
  }

  animateMascot() {
    // Ball spin
    gsap.to(this.ball.nativeElement, {
      rotate: 360,
      duration: 10,
      repeat: -1,
      ease: 'none'
    });

    // Pulse rings
    gsap.to('.pulse-ring', {
      scale: 1.5,
      opacity: 0,
      duration: 2,
      repeat: -1,
      stagger: 0.5,
      ease: 'power1.out'
    });

    // Staggered rules reveal
    gsap.from('.rule-card', {
      y: 30,
      opacity: 0,
      duration: 0.8,
      stagger: 0.2,
      ease: 'back.out(1.7)',
      delay: 0.5
    });
  }

  enterArena() {
    const tl = gsap.timeline({
      onComplete: () => this.dismissed.emit()
    });

    tl.to('.intro-container', {
      scale: 1.1,
      opacity: 0,
      duration: 0.6,
      ease: 'power2.inOut'
    });
  }
}
