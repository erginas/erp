import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu.tsx"

import type { UserPublic } from "@/client"
import DeleteUser from "@/features/Admin/components/DeleteUser.tsx"
import EditUser from "@/features/Admin/components/EditUser.tsx"

interface UserActionsMenuProps {
  user: UserPublic
  disabled?: boolean
}

export const UserActionsMenu = ({ user, disabled }: UserActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit" disabled={disabled}>
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditUser user={user} />
        <DeleteUser id={user.id} />
      </MenuContent>
    </MenuRoot>
  )
}
