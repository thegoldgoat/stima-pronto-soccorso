import { WaitingTimesType } from '../models/esteem'

export type PatientEsteemAPI = {
  waiting_times: WaitingTimesType
  emergency_code: Number
  arrival_time: Date
}
