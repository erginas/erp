import React from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
}

export function Input({ label, className = '', ...props }: InputProps) {
  return (
    <div className="flex flex-col space-y-1">
      {label && <label className="text-sm font-medium">{label}</label>}
      <input
        className={`border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300 ${className}`}
        {...props}
      />
    </div>
  )
}
