using System.ComponentModel.DataAnnotations;

public class Contacto
{
    [Key]
    public int Id { get; set; }

    [Required]
    public string Nombre { get; set; } = string.Empty;

    [Required]
    [EmailAddress]
    public string Gmail { get; set; } = string.Empty;

    [Required]
    [Phone]
    public string Telefono { get; set; } = string.Empty;
}
