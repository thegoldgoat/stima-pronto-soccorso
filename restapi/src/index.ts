const API_PORT = process.env.PORT || 8000

import express, { json, Request, Response } from 'express'
import { connect } from 'mongoose'
import cors from 'cors'

import monitorRoutes from './routes/monitor'
import patientRouter from './routes/patient'

async function main() {
  let mongoClient: typeof import('mongoose')
  try {
    console.log('Trying to connect to database...')
    mongoClient = await connect(
      process.env.DB_URI || 'mongodb://localhost:27017/stima-pronto-soccorso'
    )
    console.log('Connected to database')
  } catch (error) {
    console.error('Error while connecting to database:', error)
    process.exit(1)
  }

  var app = express()

  app.set('trust proxy', 1)

  if (process.env.NODE_ENV != 'production') {
    app.use(cors())

    app.use(async (req: Request, res: Response, next) => {
      console.log(`${req.method} ${req.url}`)
      setTimeout(next, 1000)
    })
  }

  app.use(json())

  app.use('/patient', patientRouter)
  app.use('/monitor', monitorRoutes)

  app.listen(API_PORT)
  console.log(`Listening on port ${API_PORT}`)
}

main()
