import {Button, DialogTitle, Text} from "@chakra-ui/react"
import {useMutation, useQueryClient} from "@tanstack/react-query"
import {useState} from "react"
import {useForm} from "react-hook-form"
import {FiTrash2} from "react-icons/fi"

// import { ItemsService } from "@/client"
import {KisilerService} from "../../kisiler/api/KisilerServices"
import {
    DialogActionTrigger,
    DialogBody,
    DialogCloseTrigger,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogRoot,
    DialogTrigger,
} from "../../../components/ui/dialog"
import useCustomToast from "../../../hooks/useCustomToast"

const DeleteKisi = ({kimlik_no}: { kimlik_no: number }) => {
    const [isOpen, setIsOpen] = useState(false)
    const queryClient = useQueryClient()
    const {showSuccessToast, showErrorToast} = useCustomToast()
    const {
        handleSubmit,
        formState: {isSubmitting},
    } = useForm()

    const deleteKisi = async (kimlik_no: number) => {
        await KisilerService.deleteKisi({kimlik_no: kimlik_no})
    }

    const mutation = useMutation({
        mutationFn: deleteKisi,
        onSuccess: () => {
            showSuccessToast("The item was deleted successfully")
            setIsOpen(false)
        },
        onError: () => {
            showErrorToast("An error occurred while deleting the item")
        },
        onSettled: () => {
            queryClient.invalidateQueries()
        },
    })

    const onSubmit = async () => {
        mutation.mutate(kimlik_no)
    }

    return (
        <DialogRoot
            size={{base: "xs", md: "md"}}
            placement="center"
            role="alertdialog"
            open={isOpen}
            onOpenChange={({open}) => setIsOpen(open)}
        >
            <DialogTrigger asChild>
                <Button variant="ghost" size="sm" colorPalette="red">
                    <FiTrash2 fontSize="16px"/>
                    Delete Kişi
                </Button>
            </DialogTrigger>

            <DialogContent>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <DialogCloseTrigger/>
                    <DialogHeader>
                        <DialogTitle>Delete Kişi</DialogTitle>
                    </DialogHeader>
                    <DialogBody>
                        <Text mb={4}>
                            This item will be permanently deleted. Are you sure? You will not
                            be able to undo this action.
                        </Text>
                    </DialogBody>

                    <DialogFooter gap={2}>
                        <DialogActionTrigger asChild>
                            <Button
                                variant="subtle"
                                colorPalette="gray"
                                disabled={isSubmitting}
                            >
                                Cancel
                            </Button>
                        </DialogActionTrigger>
                        <Button
                            variant="solid"
                            colorPalette="red"
                            type="submit"
                            loading={isSubmitting}
                        >
                            Delete
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </DialogRoot>
    )
}

export default DeleteKisi
