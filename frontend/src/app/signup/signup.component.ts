import { Component } from '@angular/core';
import {MatError, MatFormField, MatLabel} from "@angular/material/form-field";
import {MatOption, MatSelect} from "@angular/material/select";
import {MatDialogActions, MatDialogContent, MatDialogTitle} from "@angular/material/dialog";
import {FormsModule} from "@angular/forms";
import {MatInput} from "@angular/material/input";
import {MatButton} from "@angular/material/button";

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
    MatButton
  ],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.scss'
})
export class SignupComponent {

  signUp() {
    console.log('Sign up');
  }
}
