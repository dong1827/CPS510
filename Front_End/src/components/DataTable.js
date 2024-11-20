import React from 'react';

const DataTable = ({ columns, rows }) => {

    if (columns) {
        return (
            <div>
            <h2>Data Table</h2>
            <table border="1" cellPadding="5" cellSpacing="0">
                <thead>
                <tr>
                    {columns.map((column, index) => (
                    <th key={index}>{column}</th>
                    ))}
                </tr>
                </thead>
                <tbody>
                {rows.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                        <td key={cellIndex}>{cell}</td>
                    ))}
                    </tr>
                ))}
                </tbody>
            </table>
            </div>
        );
    }
    else {
        return ""
    }
    
};

export default DataTable;