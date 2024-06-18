import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {Router, RouterOutlet} from '@angular/router';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatToolbar} from "@angular/material/toolbar";
import {MatIcon} from "@angular/material/icon";
import {AuthService} from "./services/auth.service";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, MatSlideToggleModule, MatToolbar, MatIcon],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'angular-docker';

  isLoggedIn = false;

  constructor(
    private authService: AuthService,
    private router: Router
    ) {
  }

  ngOnInit() {
    this.isLoggedIn = this.authService.isLogged();
  }

  logout() {
    this.authService.logout().subscribe({
      next: (response: any) => {
        console.log(response);
        this.isLoggedIn = false;
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error(error);
      }
    });
  }
}
