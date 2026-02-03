export default function StatusTable({ rows, columns }) {
  if (!rows.length) {
    return <p>No data yet. Run the analysis to see results.</p>;
  }

  return (
    <table className="table">
      <thead>
        <tr>
          {columns.map((column) => (
            <th key={column.key}>{column.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, index) => (
          <tr key={`${row[columns[0].key]}-${index}`}>
            {columns.map((column) => {
              const value = row[column.key];
              if (column.key === "Status") {
                const badgeClass = value === "HIGH" ? "badge-high" : "badge-low";
                return (
                  <td key={column.key} className={badgeClass}>
                    {value}
                  </td>
                );
              }
              return <td key={column.key}>{value}</td>;
            })}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
