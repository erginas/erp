// src/components/ui/table.tsx
import React from 'react';
import {chakra, HTMLChakraProps} from '@chakra-ui/react';

// Functional wrappers around HTML table elements with Chakra styling
export const Table: React.FC<HTMLChakraProps<'table'>> = (props) => {
    return <chakra.table {...props}>{props.children}</chakra.table>;
};

export const Header: React.FC<HTMLChakraProps<'thead'>> = (props) => {
    return <chakra.thead {...props}>{props.children}</chakra.thead>;
};

export const Body: React.FC<HTMLChakraProps<'tbody'>> = (props) => {
    return <chakra.tbody {...props}>{props.children}</chakra.tbody>;
};

export const Row: React.FC<HTMLChakraProps<'tr'>> = (props) => {
    return <chakra.tr {...props}>{props.children}</chakra.tr>;
};

export const ColumnHeader: React.FC<HTMLChakraProps<'th'>> = (props) => {
    return <chakra.th {...props}>{props.children}</chakra.th>;
};

export const Cell: React.FC<HTMLChakraProps<'td'>> = (props) => {
    return <chakra.td {...props}>{props.children}</chakra.td>;
};

export const Button: React.FC<HTMLChakraProps<'button'>> = (props) => {
    return <chakra.button {...props}>{props.children}</chakra.button>;
};



