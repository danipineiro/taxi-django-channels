import {Component} from '@angular/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule} from '@angular/forms';
import {MatCard, MatCardContent} from "@angular/material/card"
import {MatButtonModule} from '@angular/material/button';
import {MatDivider} from "@angular/material/divider";
import {MatDialog} from "@angular/material/dialog";
import {SignupComponent} from "../signup/signup.component";
import {AuthService} from "../services/auth.service";


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, FormsModule, MatCard, MatCardContent, MatButtonModule, MatDivider],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  constructor(
    public dialog: MatDialog,
    private authService: AuthService
  ) {
  }

  openSingUpDialog() {
    this.dialog.open(SignupComponent, {
      width: '500px'
    });
  }
}
