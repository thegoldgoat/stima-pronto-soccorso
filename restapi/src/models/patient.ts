import { Schema, model } from 'mongoose'

interface Patient {}

const patientSchema = new Schema<Patient>({}, { collection: 'patient_model' })

const patientModel = model('patient', patientSchema)

export { patientSchema, patientModel, Patient }
