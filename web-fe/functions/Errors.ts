import { EventBus } from '@/functions/EventBus'

export async function manageError(message: string, error: any): Promise<void> {
  return new Promise((resolve) => {
    let secondmessage = error.message
    if (error.response) {
      switch (error.response.status) {
        case 403:
          secondmessage = 'Permesso negato'
          break
        case 400:
          secondmessage = 'Richiesta non valida'
          break
        case 404:
          secondmessage = 'Nessun elemento trovato'
          break
      }
    }
    EventBus.$emit('error', `${message}: ${secondmessage}`)
    resolve()
  })
}
