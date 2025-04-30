import {useMutation, useQueryClient} from "@tanstack/react-query"
import {type SubmitHandler, useForm} from "react-hook-form"

import {Button, DialogActionTrigger, DialogTitle, Input, Text, VStack,} from "@chakra-ui/react"
import {useState} from "react"
import {FaPlus} from "react-icons/fa"
import {KisilerService} from "@/modules/kisiler/api/KisilerServices"
import {type KisiCreate} from "@/modules/kisiler/types/KisiTypes"
import type {ApiError} from "@/client/core/ApiError"
import useCustomToast from "@/hooks/useCustomToast"
import {handleError} from "@/utils"
import {
    DialogBody,
    DialogCloseTrigger,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogRoot,
    DialogTrigger,
} from "@/components/ui/dialog"
import {Field} from "@/components/ui/field"


const AddItem = () => {
    const [isOpen, setIsOpen] = useState(false)
    const queryClient = useQueryClient()
    const {showSuccessToast} = useCustomToast()
    const {
        register,
        handleSubmit,
        reset,
        formState: {errors, isValid, isSubmitting},
    } = useForm<KisiCreate>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            kimlik_no: 0,
            adi: "",
            soyadi: "",
        },
    })

    const mutation = useMutation({
        mutationFn: (data: KisiCreate) =>
            KisilerService.createKisi({requestBody: data}),
        onSuccess: () => {
            showSuccessToast("Kişi Oluşturuldu.")
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

    const onSubmit: SubmitHandler<KisiCreate> = (data) => {
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
                <Button value="add-item" my={4}>
                    <FaPlus fontSize="16px"/>
                    Kişi ekle
                </Button>
            </DialogTrigger>
            <DialogContent>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <DialogHeader>
                        <DialogTitle>Kişi Ekle</DialogTitle>
                    </DialogHeader>
                    <DialogBody>
                        <Text mb={4}>Lütfen Bilgileri Doldurun.</Text>
                        <VStack gap={4}>

                            <Field
                                required
                                invalid={!!errors.kimlik_no}
                                errorText={errors.kimlik_no?.message}
                                label="Kimlik No"
                            >
                                <Input
                                    id="kimlik_no"
                                    {...register("kimlik_no", {
                                        required: "Kimlik Bilgisi zorunlu lütfen girin.",
                                    })}
                                    placeholder="Kimlik No"
                                    type="text"
                                />
                            </Field>


                            <Field
                                required
                                invalid={!!errors.adi}
                                errorText={errors.adi?.message}
                                label="Adı"
                            >
                                <Input
                                    id="adi"
                                    {...register("adi", {
                                        required: "İsim bilgisi zorunlu lütfen girin.",
                                    })}
                                    placeholder="Adı"
                                    type="text"
                                />
                            </Field>

                            <Field
                                invalid={!!errors.soyadi}
                                errorText={errors.soyadi?.message}
                                label="soyadi"
                            >
                                <Input
                                    id="soyadi"
                                    {...register("soyadi")}
                                    placeholder="Soaydi"
                                    type="text"
                                />
                            </Field>
                        </VStack>
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
                            type="submit"
                            disabled={!isValid}
                            loading={isSubmitting}
                        >
                            Save
                        </Button>
                    </DialogFooter>
                </form>
                <DialogCloseTrigger/>
            </DialogContent>
        </DialogRoot>
    )
}

export default AddItem
