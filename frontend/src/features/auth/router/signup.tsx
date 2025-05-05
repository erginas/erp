// src/routes/signup.tsx

import {createRoute, redirect} from "@tanstack/react-router";
import SignUpPage from "@/features/auth/components/SignUpPage"; // Bu dosyayı da oluşturmalısınız
import {isLoggedIn} from "@/shared/hooks/useAuth";
import {rootRoute} from "@/routes/routeTree.tsx";

export const signupRoute = createRoute({
    path: "/signup",
    getParentRoute: () => rootRoute,
    component: SignUpPage,
    beforeLoad: async () => {
        // Eğer zaten giriş yapılmışsa direkt ana sayfaya gönder
        if (isLoggedIn()) {
            throw redirect({to: "/"});
        }
    },
});


// import { Container, Flex, Image, Input, Text } from "@chakra-ui/react"
// import {
//   Link as RouterLink,
//   createFileRoute,
//   redirect,
// } from "@tanstack/react-router"
// import { type SubmitHandler, useForm } from "react-hook-form"
// import { FiLock, FiUser } from "react-icons/fi"
//
// import type { UserRegister } from "@/client"
// import { Button } from "@/components/ui/button"
// import { Field } from "@/components/ui/field"
// import { InputGroup } from "@/components/ui/input-group"
// import { PasswordInput } from "@/components/ui/password-input"
// import useAuth, { isLoggedIn } from "@/hooks/useAuth"
// import { confirmPasswordRules, emailPattern, passwordRules } from "@/utils"
// import Logo from "/assets/images/fastapi-logo.svg"
//
// export const Route = createFileRoute("/signup")({
//   component: SignUp,
//   beforeLoad: async () => {
//     if (isLoggedIn()) {
//       throw redirect({
//         to: "/",
//       })
//     }
//   },
// })
//
// interface UserRegisterForm extends UserRegister {
//   confirm_password: string
// }
//
// function SignUp() {
//   const { signUpMutation } = useAuth()
//   const {
//     register,
//     handleSubmit,
//     getValues,
//     formState: { errors, isSubmitting },
//   } = useForm<UserRegisterForm>({
//     mode: "onBlur",
//     criteriaMode: "all",
//     defaultValues: {
//       email: "",
//       full_name: "",
//       password: "",
//       confirm_password: "",
//     },
//   })
//
//   const onSubmit: SubmitHandler<UserRegisterForm> = (data) => {
//     signUpMutation.mutate(data)
//   }
//
//   return (
//     <>
//       <Flex flexDir={{ base: "column", md: "row" }} justify="center" h="100vh">
//         <Container
//           as="form"
//           onSubmit={handleSubmit(onSubmit)}
//           h="100vh"
//           maxW="sm"
//           alignItems="stretch"
//           justifyContent="center"
//           gap={4}
//           centerContent
//         >
//           <Image
//             src={Logo}
//             alt="FastAPI logo"
//             height="auto"
//             maxW="2xs"
//             alignSelf="center"
//             mb={4}
//           />
//           <Field
//             invalid={!!errors.full_name}
//             errorText={errors.full_name?.message}
//           >
//             <InputGroup w="100%" startElement={<FiUser />}>
//               <Input
//                 id="full_name"
//                 minLength={3}
//                 {...register("full_name", {
//                   required: "Full Name is required",
//                 })}
//                 placeholder="Full Name"
//                 type="text"
//               />
//             </InputGroup>
//           </Field>
//
//           <Field invalid={!!errors.email} errorText={errors.email?.message}>
//             <InputGroup w="100%" startElement={<FiUser />}>
//               <Input
//                 id="email"
//                 {...register("email", {
//                   required: "Email is required",
//                   pattern: emailPattern,
//                 })}
//                 placeholder="Email"
//                 type="email"
//               />
//             </InputGroup>
//           </Field>
//           <PasswordInput
//             type="password"
//             startElement={<FiLock />}
//             {...register("password", passwordRules())}
//             placeholder="Password"
//             errors={errors}
//           />
//           <PasswordInput
//             type="confirm_password"
//             startElement={<FiLock />}
//             {...register("confirm_password", confirmPasswordRules(getValues))}
//             placeholder="Confirm Password"
//             errors={errors}
//           />
//           <Button variant="solid" type="submit" loading={isSubmitting}>
//             Sign Up
//           </Button>
//           <Text>
//             Already have an account?{" "}
//             <RouterLink to="/login" className="main-link">
//               Log In
//             </RouterLink>
//           </Text>
//         </Container>
//       </Flex>
//     </>
//   )
// }
//
// export default SignUp
