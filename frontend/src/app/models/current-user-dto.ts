import {DRIVER, PASSENGER} from "../shared/constants/user-types";

export enum UserType {
  Driver = DRIVER,
  Passenger = PASSENGER
}
export interface CurrentUserDTO {
  email: string;
  email_verified: boolean;
  is_active: boolean;
  type: UserType
}
