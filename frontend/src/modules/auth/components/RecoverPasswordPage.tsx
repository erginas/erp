import {Flex, Heading, Input, Text,} from "@chakra-ui/react";
import {useMutation} from "@tanstack/react-query";
import {SubmitHandler, useForm} from "react-hook-form";
import {FiMail} from "react-icons/fi";

import {type ApiError, LoginService} from "@/client";
import {Button} from "@/components/ui/button";
import {Field} from "@/components/ui/field";
import {InputGroup} from "@/components/ui/input-group";
import useCustomToast from "@/hooks/useCustomToast";
import {emailPattern, handleError} from "@/utils";

interface FormData {
    email: string;
}

export default function RecoverPasswordPage() {
    const {
        register,
        handleSubmit,
        reset,
        formState: {errors, isSubmitting},
    } = useForm<FormData>();

    const {showSuccessToast} = useCustomToast();

    const mutation = useMutation<void, ApiError, FormData>({
        mutationFn: (data) => LoginService.recoverPassword({email: data.email}),
        onSuccess: () => {
            showSuccessToast("Password recovery email sent successfully.");
            reset();
        },
        onError: handleError,
    });

    const onSubmit: SubmitHandler<FormData> = (data) => {
        if (!isSubmitting) {
            mutation.mutate(data);
        }
    };

    return (
        <Flex
            as="form"
            onSubmit={handleSubmit(onSubmit)}
            direction="column"
            h="100vh"
            maxW="sm"
            m="auto"
            justify="center"
            gap={4}
        >
            <Heading size="xl" textAlign="center">
                Password Recovery
            </Heading>
            <Text textAlign="center">
                A password recovery email will be sent to the registered account.
            </Text>

            <Field invalid={!!errors.email} errorText={errors.email?.message}>
                <InputGroup startElement={<FiMail/>}>
                    <Input
                        id="email"
                        placeholder="Email"
                        type="email"
                        {...register("email", {
                            required: "Email is required",
                            pattern: {
                                value: emailPattern.value,
                                message: emailPattern.message,
                            },
                        })}
                    />
                </InputGroup>
            </Field>

            <Button variant="solid" type="submit" loading={isSubmitting}>
                Continue
            </Button>
        </Flex>
    );
}
