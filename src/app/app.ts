import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { MascotIntroComponent } from './components/mascot-intro/mascot-intro';
import { NavbarComponent } from './components/layout/navbar/navbar';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, MascotIntroComponent, NavbarComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent {
  showIntro = true;

  onIntroDismissed() {
    this.showIntro = false;
    // Persist in session storage if needed
    sessionStorage.setItem('introDismissed', 'true');
  }

  constructor() {
    if (sessionStorage.getItem('introDismissed') === 'true') {
      this.showIntro = false;
    }
  }
}
