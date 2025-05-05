// src/modules/auth/components/SignUpPage.tsx
import {Flex, Input, Text} from "@chakra-ui/react";
import {SubmitHandler, useForm} from "react-hook-form";
import {Link as RouterLink} from "@tanstack/react-router";
import {Button} from "@/shared/components/ui/Button.tsx";
import useAuth from "@/shared/hooks/useAuth.ts";

interface SignUpData {
    email: string;
    password: string;
    full_name?: string;
}

export default function SignUpPage() {
    const {signUpMutation, error} = useAuth();
    const {register, handleSubmit, formState} = useForm<SignUpData>();

    const onSubmit: SubmitHandler<SignUpData> = async (data) => {
        await signUpMutation.mutateAsync(data);
    };

    return (
        <Flex as="form" direction="column" gap={4} maxW="sm" m="auto" pt={12}>
            <Text fontSize="2xl">Create your account</Text>
            <Input placeholder="Full Name" {...register("full_name")} />
            <Input
                placeholder="Email"
                type="email"
                {...register("email", {required: true})}
            />
            <Input
                placeholder="Password"
                type="password"
                {...register("password", {required: true})}
            />
            {error && <Text color="red.500">{error}</Text>}
            <Button type="submit" loading={formState.isSubmitting}>
                Sign Up
            </Button>
            <Text>
                Already have an account?{" "}
                <RouterLink to="/login" className="main-link">
                    Log In
                </RouterLink>
            </Text>
        </Flex>
    );
}
