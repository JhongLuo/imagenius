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

  const blinkToast = async (domId: string, type: ToastType, text: string) => {
    // toast is hidden by default
    const newToast = {
      uuid: uuidv4(),
      domId,
      isShown: false,
      type,
      text,
    } as ToastModel
    toastsArray.value.push(newToast)

    const findAndShowToast = () => {
      const theToast = toastsArray.value.find(t => t.uuid === newToast.uuid)!
      theToast.isShown = true
    }

    const findAndHideToast = () => {
      const theToast = toastsArray.value.find(t => t.uuid === newToast.uuid)!
      theToast.isShown = false
    }

    // show toast with delay, for the animation to work
    await utils.sleep(1)
    findAndShowToast()

    // hide toast after 3.5 seconds
    await utils.sleep(3500)
    findAndHideToast()
  }

  return {
    toastsArray,
    blinkToast,
  }
}
