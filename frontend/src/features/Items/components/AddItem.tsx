import {useMutation, useQueryClient} from "@tanstack/react-query"
import {type SubmitHandler, useForm} from "react-hook-form"

import {Button, DialogActionTrigger, DialogTitle, Input, Text, VStack,} from "@chakra-ui/react"
import {useState} from "react"
import {FaPlus} from "react-icons/fa"

import {type KisiCreate} from "@/features/hr/types/KisiTypes.ts"
import {KisilerService} from "@/features/kisiler/api/KisilerServices.ts"
import type {ApiError} from "@/client/core/client/ApiError.ts"
import useCustomToast from "@/shared/hooks/useCustomToast.ts"
import {handleError} from "@/utils.ts"
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTrigger,
} from "../../../shared/components/ui/dialog.tsx"
import {Field} from "../../../shared/components/ui/field.tsx"

const AddKisi = () => {
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
            adi: "",
            soyadi: "",
        },
    })

    const mutation = useMutation({
        mutationFn: (data: KisiCreate) =>
            KisilerService.createKisi({requestBody: data}),
        onSuccess: () => {
            showSuccessToast("Item created successfully.")
            reset()
            setIsOpen(false)
        },
        onError: (err: ApiError) => {
            handleError(err)
        },
        onSettled: () => {
            queryClient.invalidateQueries({queryKey: ["items"]})
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
                    Add Item
                </Button>
            </DialogTrigger>
            <DialogContent>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <DialogHeader>
                        <DialogTitle>Add Item</DialogTitle>
                    </DialogHeader>
                    <DialogBody>
                        <Text mb={4}>Fill in the details to add a new item.</Text>
                        <VStack gap={4}>
                            <Field
                                required
                                invalid={!!errors.adi}
                                errorText={errors.adi?.message}
                                label="Title"
                            >
                                <Input
                                    id="title"
                                    {...register("adi", {
                                        required: "Adı is required.",
                                    })}
                                    placeholder="adi"
                                    type="text"
                                />
                            </Field>

                            <Field
                                invalid={!!errors.soyadi}
                                errorText={errors.soyadi?.message}
                                label="Soyadı"
                            >
                                <Input
                                    id="description"
                                    {...register("soyadi")}
                                    placeholder="Soyadı"
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

export default AddKisi
