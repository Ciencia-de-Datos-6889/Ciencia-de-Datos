using Microsoft.EntityFrameworkCore;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) 
        : base(options) { }

    public DbSet<Contacto> Contactos { get; set; } = null!;
    public DbSet<Usuario> Usuarios { get; set; } = null!;
}
