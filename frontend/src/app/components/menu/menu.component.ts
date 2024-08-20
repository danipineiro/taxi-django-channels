import {Component, OnInit} from '@angular/core';
import {MatIcon} from "@angular/material/icon";
import {MatToolbar} from "@angular/material/toolbar";
import {NgIf} from "@angular/common";
import {AuthService} from "../../services/auth.service";
import {Router} from "@angular/router";
import {UserService} from "../../services/user.service";
import {CurrentUserDTO} from "../../models/current-user-dto";

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [
    MatIcon,
    MatToolbar,
    NgIf
  ],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.scss'
})
export class MenuComponent implements OnInit {

  currentUser: CurrentUserDTO | undefined;

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private router: Router
  ) {
  }

  ngOnInit() {
    this.userService.getCurrentUser().subscribe({
        next: (user: CurrentUserDTO) => {
          this.currentUser = user;
        },
      }
    )
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

}
