import {DRIVER, PASSENGER} from "../shared/constants/user-types";

export enum UserType {
  Driver = DRIVER,
  Passenger = PASSENGER
}

export interface RegisterDTO {
  email: string;
  password: string;
  user_type: UserType;
}