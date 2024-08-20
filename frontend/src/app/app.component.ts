import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {Router, RouterOutlet} from '@angular/router';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatToolbar} from "@angular/material/toolbar";
import {MatIcon} from "@angular/material/icon";
import {AuthService} from "./services/auth.service";
import {MenuComponent} from "./components/menu/menu.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, MatSlideToggleModule, MatToolbar, MatIcon, MenuComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'angular-docker';

  isLoggedIn = false;

  constructor(
    private authService: AuthService,
  ) {
  }

  ngOnInit() {
    this.authService.loggedChanged$.subscribe(isLogged => this.isLoggedIn = isLogged);

    this.isLoggedIn = this.authService.isLogged();
  }
}
