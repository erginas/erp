import {Button, ButtonGroup, DialogActionTrigger, Input, Text, VStack,} from "@chakra-ui/react"
import {useMutation, useQueryClient} from "@tanstack/react-query"
import {useState} from "react"
import {type SubmitHandler, useForm} from "react-hook-form"
import {FaExchangeAlt} from "react-icons/fa"

// import { type ApiError, type ItemPublic, ItemsService } from "@/client"
import {type ApiError} from "../../../client"

import {type KisiPublic} from "../../kisiler/types/KisiTypes"

import {KisilerService} from "../../kisiler/api/KisilerServices"


import useCustomToast from "../../../hooks/useCustomToast"
import {handleError} from "../../../utils"
import {
    DialogBody,
    DialogCloseTrigger,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogRoot,
    DialogTitle,
    DialogTrigger
} from "../../../components/ui/dialog"
import {Field} from "../../../components/ui/field"

import {Checkbox} from "../../../components/ui/checkbox"

interface EditKisiProps {
    kisi: KisiPublic
}

interface KisiUpdateForm {
    adi: string
    soyadi?: string
    is_active?: boolean
}

const EditKisi = ({kisi}: EditKisiProps) => {
    const [isOpen, setIsOpen] = useState(false)
    const queryClient = useQueryClient()
    const {showSuccessToast} = useCustomToast()
    const {
        register,
        handleSubmit,
        reset,
        formState: {errors, isSubmitting},
    } = useForm<KisiUpdateForm>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            ...kisi,
            soyadi: kisi.soyadi ?? undefined,
        },
    })

    const mutation = useMutation({
        mutationFn: (data: KisiUpdateForm) =>
            KisilerService.updateKisi({kimlik_no: kisi.kimlik_no, requestBody: data}),
        onSuccess: () => {
            showSuccessToast("Kişi bilgileri başarılı bir şekilde güncellendi.")
            reset()
            setIsOpen(false)
        },
        onError: (err: ApiError) => {
            handleError(err)
        },
        onSettled: () => {
            queryClient.invalidateQueries({queryKey: ["kisiler"]})
        },
    })

    const onSubmit: SubmitHandler<KisiUpdateForm> = async (data) => {
        mutation.mutate(data)
    }

    return (
        <DialogRoot
            size={{base: "xs", md: "md"}}
            placement="center"
            open={isOpen}
            onOpenChange={({open}) => setIsOpen(open)}
        >
            <DialogTrigger asChild>
                <Button variant="ghost">
                    <FaExchangeAlt fontSize="16px"/>
                    Edit Item
                </Button>
            </DialogTrigger>
            <DialogContent>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <DialogHeader>
                        <DialogTitle>Edit Kisi</DialogTitle>
                    </DialogHeader>
                    <DialogBody>
                        <Text mb={4}>Update the item details below.</Text>
                        <VStack gap={4}>
                            <Field
                                required
                                invalid={!!errors.adi}
                                errorText={errors.adi?.message}
                                label="Title"
                            >
                                <Input
                                    id="adi"
                                    {...register("adi", {
                                        required: "Adı is required",
                                    })}
                                    placeholder="Adı"
                                    type="text"
                                />
                            </Field>

                            <Field
                                invalid={!!errors.soyadi}
                                errorText={errors.soyadi?.message}
                                label="Soyadi"
                            >
                                <Input
                                    id="soyadi"
                                    {...register("soyadi")}
                                    placeholder="Soyadi"
                                    type="text"
                                />
                            </Field>

                            <Checkbox
                                // required
                                // invalid={!!errors.is_active}
                                // // errorText={errors.is_active?.message}
                                // label="Aktif"
                            >
                                <Input
                                    id="is_active"
                                    {...register("is_active")}
                                    placeholder="is_active"
                                    type="checkbox"
                                />
                            </Checkbox>
                        </VStack>
                    </DialogBody>

                    <DialogFooter gap={2}>
                        <ButtonGroup>
                            <DialogActionTrigger asChild>
                                <Button
                                    variant="subtle"
                                    colorPalette="gray"
                                    disabled={isSubmitting}
                                >
                                    Cancel
                                </Button>
                            </DialogActionTrigger>
                            <Button variant="solid" type="submit" loading={isSubmitting}>
                                Save
                            </Button>
                        </ButtonGroup>
                    </DialogFooter>
                </form>
                <DialogCloseTrigger/>
            </DialogContent>
        </DialogRoot>
    )
}

export default EditKisi
