import {Component, OnInit} from '@angular/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {MatCard, MatCardContent} from "@angular/material/card"
import {MatButtonModule} from '@angular/material/button';
import {MatDivider} from "@angular/material/divider";
import {MatDialog} from "@angular/material/dialog";
import {SignupComponent} from "./signup/signup.component";
import {AuthService} from "../../services/auth.service";
import {LoginResponseDTO} from "../../models/login-response-dto";
import {Router} from "@angular/router";


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, FormsModule, MatCard, MatCardContent, MatButtonModule, MatDivider, ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent implements OnInit {

  loginForm!: FormGroup;

  constructor(
    public dialog: MatDialog,
    private authService: AuthService,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      email: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required])
    });
  }

  login() {
    const loginDTO = this.loginForm.value;
    this.authService.login(loginDTO).subscribe({
        next: (response: LoginResponseDTO) => {
          this.authService.setAccessToken(response.access);
          this.authService.setRefreshToken(response.refresh);
          this.router.navigate(['/']);
        },
        error: (error) => {
          console.error(error);
        }
      }
    );
  }

  openSingUpDialog() {
    this.dialog.open(SignupComponent, {
      width: '500px'
    });
  }
}
