import {Component, OnInit} from '@angular/core';
import {MatError, MatFormField, MatLabel} from "@angular/material/form-field";
import {MatOption, MatSelect} from "@angular/material/select";
import {MatDialogActions, MatDialogContent, MatDialogTitle} from "@angular/material/dialog";
import {
  AbstractControl,
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";
import {MatInput} from "@angular/material/input";
import {MatButton} from "@angular/material/button";
import {NgIf} from "@angular/common";
import {DRIVER, PASSENGER} from "../shared/constants/user-types";
import {RegisterDTO} from "../models/register-dto";
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [
    MatFormField,
    MatSelect,
    MatOption,
    MatError,
    MatDialogActions,
    MatLabel,
    MatDialogContent,
    MatDialogTitle,
    FormsModule,
    MatInput,
    MatButton,
    ReactiveFormsModule,
    NgIf
  ],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.scss'
})
export class SignupComponent implements OnInit {

  signupForm!: FormGroup;
  driver = DRIVER;
  passenger = PASSENGER;

  constructor(
    private authService: AuthService
  ) {
  }

  ngOnInit() {
    this.signupForm = new FormGroup({
      username: new FormControl('', [Validators.required, Validators.email]),
      user_type: new FormControl(this.passenger, Validators.required),
      password: new FormControl('', Validators.required),
      confirmPassword: new FormControl('', Validators.required)
    }, [this.checkPasswords]);
  }

  checkPasswords(group: AbstractControl) {
    if (group.get('password')?.value !== group.get('confirmPassword')?.value) {
      return {notSame: true};
    }
    return null;
  }

  signUp() {
    const registrationData: RegisterDTO = this.signupForm.value;
    console.log(registrationData);
    this.authService.register(registrationData).subscribe({
        next: () => {
          console.log('User registered');
        },
        error: (error) => {
          console.error('There was an error!', error);
        },
        complete: () => {
          console.log('Registration completed');
        }
      }
    );
  }

}
