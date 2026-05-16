import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class NavbarComponent {
  navLinks = [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/predict', label: 'Predict' },
    { path: '/fantasy', label: 'Fantasy' },
    { path: '/leaderboard', label: 'Leaderboard' },
    { path: '/xp', label: 'XP' },
    { path: '/ai-coach', label: 'Coach' },
    { path: '/admin', label: 'Admin' },
    { path: '/docs', label: 'Docs' }
  ];
}
