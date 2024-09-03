import {ACCEPTED, COMPLETED, REQUESTED, STARTED} from "../shared/constants/trip-status";

export enum tripStatus {
    Requested = REQUESTED,
    Accepted = ACCEPTED,
    Started = STARTED,
    Completed = COMPLETED
}

export interface Trip {
  id: number;
  source_latitude: number | null;
  source_longitude: number | null;
  destination_latitude: number | null;
  destination_longitude: number | null;
  status: tripStatus;
  driver: string;
  passenger: string;
  created: string;
  modified: string;
}
