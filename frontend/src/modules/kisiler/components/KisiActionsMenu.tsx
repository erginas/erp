import {IconButton} from "@chakra-ui/react"
import {BsThreeDotsVertical} from "react-icons/bs"
// import {MenuContent, MenuRoot, MenuTrigger} from "@/ /ui/menu"
import type {KisiPublic} from "@/modules/kisiler/types/KisiTypes"

import DeleteKisi from "@/modules/kisiler/components/DeleteKisi"
import EditKisi from "@/modules/kisiler/components/EditKisi"
import {MenuContent, MenuRoot, MenuTrigger} from "@/components/ui/menu.tsx";

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
