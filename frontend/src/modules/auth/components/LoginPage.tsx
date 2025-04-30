// src/modules/auth/components/LoginPage.tsx

import React from "react";
import {Container, Image, Input, Text,} from "@chakra-ui/react";
import {SubmitHandler, useForm} from "react-hook-form";
import {FiLock, FiMail} from "react-icons/fi";
import {createFileRoute, redirect, useNavigate} from "@tanstack/react-router";

import {Button} from "@/components/ui/button";
import {Field} from "@/components/ui/field";
import {InputGroup} from "@/components/ui/input-group";
import useAuth, {isLoggedIn} from "@/hooks/useAuth";
import Logo from "../../../../public/assets/images/fastapi-logo.svg";

// 1️⃣ Route tanımı
export const Route = createFileRoute("/login")({
    component: LoginPage,
    beforeLoad: async () => {
        if (isLoggedIn()) {
            throw redirect({to: "/"});
        }
    },
});

interface FormValues {
    username: string;
    password: string;
}

export default function LoginPage() {
    const {loginMutation, error, resetError} = useAuth();
    const {
        register,
        handleSubmit,
        formState: {errors, isSubmitting},
    } = useForm<FormValues>({
        mode: "onBlur",
        defaultValues: {username: "", password: ""},
    });

    // 2️⃣ Global useNavigate ile yönlendirme
    const navigate = useNavigate({from: Route.id});

    const onSubmit: SubmitHandler<FormValues> = async (data) => {
        resetError();
        try {
            const token = await loginMutation.mutateAsync({
                username: data.username,
                password: data.password,
            });
            // giriş başarılıysa ana sayfaya gönder
            navigate({to: "/"});
        } catch {
            // hata useAuth hook’u tarafından işlenecek
        }
    };

    return (
        <Container
            as="form"
            onSubmit={handleSubmit(onSubmit)}
            h="100vh"
            maxW="sm"
            display="flex"
            flexDir="column"
            justifyContent="center"
            gap={4}
        >
            <Image src={Logo} alt="FastAPI logo" mb={4}/>
            <Field invalid={!!errors.username || !!error} errorText={errors.username?.message || error}>
                <InputGroup startElement={<FiMail/>}>
                    <Input
                        {...register("username", {required: "Email is required"})}
                        placeholder="Email"
                        type="email"
                    />
                </InputGroup>
            </Field>

            <Field invalid={!!errors.password} errorText={errors.password?.message}>
                <InputGroup startElement={<FiLock/>}>
                    <Input
                        {...register("password", {required: "Password is required"})}
                        placeholder="Password"
                        type="password"
                    />
                </InputGroup>
            </Field>

            <Text textAlign="right">
                <Text
                    as="span"
                    color="blue.500"
                    cursor="pointer"
                    onClick={() => navigate({to: "/recover-password"})}
                >
                    Forgot Password?
                </Text>
            </Text>

            <Button type="submit" loading={isSubmitting}>
                Log In
            </Button>

            <Text textAlign="center">
                Don't have an account?{" "}
                <Text
                    as="span"
                    color="blue.500"
                    cursor="pointer"
                    onClick={() => navigate({to: "/signup"})}
                >
                    Sign Up
                </Text>
            </Text>
        </Container>
    );
}
