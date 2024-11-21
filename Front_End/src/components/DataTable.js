import React from 'react';

const DataTable = ({ columns, rows }) => {

    // If columns is not empty, display a table
    if (columns) {
        return (
            <div>
            <h2>Data Table</h2>
            <table border="1" cellPadding="5" cellSpacing="0">
                <thead>
                {/*Create a table row for columns(each attribute)*/}
                <tr>
                    {columns.map((column, index) => (
                    <th key={index}>{column}</th>
                    ))}
                </tr>
                </thead>
                <tbody>
                {/*Create a row for each record in database*/}
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