import React from 'react'
import {headers} from './Auth'

export function Contract({ contract, user, setReload}) {
    const Accept = async (e) => {
        const res = await fetch(`api/contract/accept/${contract.id}/`, {
            method: 'PATCH',
            headers: headers
        })
        setReload(c => c + 1)
    }
    const Cancel = async () => {
        const res = await fetch(`api/contract/cancel/${contract.id}/`, {
            method: 'PATCH',
            headers: headers
        })
        setReload(c => c + 1)
    }
    const Retrieve = async () => {
        const res = await fetch(`api/contract/retrieve/${contract.id}/`, {
            method: 'PATCH',
            headers: headers
        })
        setReload(c => c + 1)
    }

    return (
        <p>
            {user.is_staff && <span>by: {contract.user} |</span>}
            <span> {contract.book} | </span>
            <small> status: {contract.status} until {contract.expiry} </small> 
            <span>
            {user.is_staff && contract.status === 'waiting' && <button onClick={Accept}>Accept</button>}
            {user.is_staff && (contract.status === 'active' || contract.status === 'late') && <button onClick={Retrieve}>Retrieve</button>}
            {contract.status === 'waiting' && <button onClick={Cancel}>Cancel</button>}
            </span>
        </p>
    )
}