import {Component, OnInit} from '@angular/core';
import {MatIcon} from "@angular/material/icon";
import {MatToolbar} from "@angular/material/toolbar";
import {NgIf} from "@angular/common";
import {AuthService} from "../../services/auth.service";
import {Router} from "@angular/router";
import {UserService} from "../../services/user.service";

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

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private router: Router
  ) {
  }

  ngOnInit() {
    this.userService.getCurrentUser().subscribe((response: any) => {
      console.log(response);
    })
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

}
