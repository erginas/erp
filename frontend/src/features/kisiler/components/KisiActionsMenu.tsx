import {IconButton} from "@chakra-ui/react"
import {BsThreeDotsVertical} from "react-icons/bs"
// import {MenuContent, MenuRoot, MenuTrigger} from "@/ /ui/menu"
import type {KisiPublic} from "@/features/hr/types/KisiTypes.ts"

import DeleteKisi from "@/features/kisiler/components/DeleteKisi.tsx"
import EditKisi from "@/features/kisiler/components/EditKisi.tsx"
import {MenuContent, MenuRoot, MenuTrigger} from "@/shared/components/ui/menu.tsx";

interface KisiActionsMenuProps {
    kisi: KisiPublic
}

export const KisiActionsMenu = ({kisi}: KisiActionsMenuProps) => {
    return (
        <MenuRoot>
            <MenuTrigger asChild>
                <IconButton variant="ghost" color="inherit">
                    <BsThreeDotsVertical/>
                </IconButton>
            </MenuTrigger>
            <MenuContent>
                <EditKisi kisi={kisi}/>
                <DeleteKisi kimlik_no={kisi.kimlik_no}/>
            </MenuContent>
        </MenuRoot>
    )
}
