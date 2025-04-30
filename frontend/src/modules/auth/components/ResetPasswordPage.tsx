import {Flex, Heading, Input,} from "@chakra-ui/react";
import {useMutation} from "@tanstack/react-query";
import {SubmitHandler, useForm} from "react-hook-form";
import {FiLock} from "react-icons/fi";

import {type ApiError, LoginService} from "@/client";
import {Button} from "@/components/ui/button";
import {Field} from "@/components/ui/field";
import {InputGroup} from "@/components/ui/input-group";
import useCustomToast from "@/hooks/useCustomToast";
import {handleError, passwordRules} from "@/utils";

interface FormData {
    token: string;
    new_password: string;
}

export default function ResetPasswordPage() {
    const {register, handleSubmit, formState: {errors, isSubmitting}, reset} = useForm<FormData>();
    const {showSuccessToast} = useCustomToast();

    const mutation = useMutation<void, ApiError, FormData>({
        mutationFn: data => LoginService.resetPassword({
            token: data.token,
            new_password: data.new_password,
        }),
        onSuccess: () => {
            showSuccessToast("Password has been reset successfully.");
            reset();
        },
        onError: handleError,
    });

    const onSubmit: SubmitHandler<FormData> = data => {
        if (!isSubmitting) mutation.mutate(data);
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
                Reset Password
            </Heading>
            <Field invalid={!!errors.token} errorText={errors.token?.message}>
                <InputGroup startElement={<FiLock/>}>
                    <Input
                        id="token"
                        placeholder="Reset Token"
                        {...register("token", {required: "Token is required"})}
                    />
                </InputGroup>
            </Field>
            <Field invalid={!!errors.new_password} errorText={errors.new_password?.message}>
                <InputGroup startElement={<FiLock/>}>
                    <Input
                        id="new_password"
                        placeholder="New Password"
                        type="password"
                        {...register("new_password", passwordRules())}
                    />
                </InputGroup>
            </Field>
            <Button type="submit" loading={isSubmitting}>
                Reset Password
            </Button>
        </Flex>
    );
}
