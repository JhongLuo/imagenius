import { v4 as uuidv4 } from 'uuid'

export interface ToastModel {
  uuid: string
  domId: string
  isShown: boolean
  type: ToastType
  text: string
}

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export function useToasts() {
  const toastsArray = ref<ToastModel[]>([])

  const blinkToast = (domId: string, type: 'success' | 'error' | 'warning', text: string) => {
    // toast is hidden by default
    const toast = {
      uuid: uuidv4(),
      domId,
      isShown: false,
      type,
      text,
    } as ToastModel
    toastsArray.value.push(toast)

    const findAndShowToast = () => {
      const theToast = toastsArray.value.find(t => t.uuid === toast.uuid)!
      theToast.isShown = true
    }

    const findAndHideToast = () => {
      const theToast = toastsArray.value.find(t => t.uuid === toast.uuid)!
      theToast.isShown = false
    }

    // manually show toast with delay, for the animation to work
    setTimeout(() => {
      findAndShowToast()
    }, 1)

    // hide toast after 4 seconds
    return new Promise((resolve) => {
      setTimeout(() => {
        findAndHideToast()
        resolve('')
      }, 4000)
    })
  }

  return {
    toastsArray,
    blinkToast,
  }
}
