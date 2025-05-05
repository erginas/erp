// shared/components/ui/Card.tsx
import React from 'react'
import classNames from 'classnames'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
}

export function Card({className = '', children, ...props}: CardProps) {
    return (
        <div
            className={classNames('bg-white rounded-lg shadow-sm', className)}
            {...props}
        >
            {children}
        </div>
    )
}

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
}

export function CardHeader({className = '', children, ...props}: CardHeaderProps) {
    return (
        <div
            className={classNames('border-b px-4 py-2 bg-gray-50 rounded-t-lg', className)}
            {...props}
        >
            {children}
        </div>
    )
}

export interface CardBodyProps extends React.HTMLAttributes<HTMLDivElement> {
}

export function CardBody({className = '', children, ...props}: CardBodyProps) {
    return (
        <div
            className={classNames('p-4', className)}
            {...props}
        >
            {children}
        </div>
    )
}
