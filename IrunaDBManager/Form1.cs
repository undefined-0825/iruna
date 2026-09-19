using System.Data;
using Microsoft.Data.Sqlite;

namespace IrunaDBManager
{
    public partial class Form1 : Form
    {
        private readonly string _connectionString = "Data Source=C:\\dev\\iruna\\iruna.db";

        public Form1()
        {
            InitializeComponent();
        }

        private async void Form1_Load(object sender, EventArgs e)
        {
            var equipList = await GetEquipsAsync(_connectionString);

            // 1. 列の自動生成を有効化
            dataGridView1.AutoGenerateColumns = true;

            // 2. DataGridView に BindingSource を明示的に接続
            dataGridView1.DataSource = bindingSource1;

            // 3. データをセット
            bindingSource1.DataSource = equipList;
        }


        public async Task<List<EquipDto>> GetEquipsAsync(string connectionString)
        {
            var list = new List<EquipDto>();

            await using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            await using var command = connection.CreateCommand();
            command.CommandText = @"
SELECT 
    id, 
    type, 
    name, 
    t_ds, 
    t_ds_normalized 
FROM equip";

            await using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                list.Add(new EquipDto
                {
                    Id = reader.GetInt32(0),
                    Type = reader.IsDBNull(1) ? 0 : reader.GetInt32(1),
                    Name = reader.IsDBNull(2) ? string.Empty : reader.GetString(2),
                    // 数値(Int64)が混ざっていても安全に文字列化
                    T_Ds = reader.IsDBNull(3) ? null : reader.GetValue(3).ToString(),
                    T_Ds_Normalized = reader.IsDBNull(4) ? null : reader.GetValue(4).ToString()
                });
            }

            return list;
        }

        public async Task UpdateNormalizedDsAsync(string connectionString, int id, string? dsNormalized)
        {
            await using var connection = new SqliteConnection(connectionString);
            await connection.OpenAsync();

            await using var command = connection.CreateCommand();
            command.CommandText = @"
UPDATE equip 
SET ds_normalized = $dsNormalized 
WHERE id = $id";

            // パラメータバインド（NULLの場合は DBNull.Value を設定）
            command.Parameters.AddWithValue("$dsNormalized", (object?)dsNormalized ?? DBNull.Value);
            command.Parameters.AddWithValue("$id", id);

            await command.ExecuteNonQueryAsync();
        }
    }

    public class EquipDto
    {
        public int Id { get; set; }
        public int Type { get; set; }
        public string Name { get; set; } = string.Empty;

        // DB からの生データ（long でも string でも受け取る）
        public object? T_Ds { get; set; }
        public object? T_Ds_Normalized { get; set; }

        // 画面バインド用（文字列として取得）
        public string DisplayTDs => T_Ds?.ToString() ?? string.Empty;
        public string DisplayTDsNormalized => T_Ds_Normalized?.ToString() ?? string.Empty;
    }
}
