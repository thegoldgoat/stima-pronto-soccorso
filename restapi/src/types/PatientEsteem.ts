import { Esteem } from '../models/esteem'

export type PatientEsteem = Esteem & {
  emergency_code: Number
  arrival_time: Date
}
