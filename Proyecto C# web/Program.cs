using System.Configuration;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Configuración de la base de datos (esto ya lo tienes)
var ConnectionString = builder.Configuration.GetConnectionString("DefaultConnection");

if (string.IsNullOrEmpty(ConnectionString))
{
    throw new InvalidOperationException("Conexión a la base de datos no encontrada");
}

// Agregar DbContext para SQL Server
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(ConnectionString));  // Cambiado a UseSqlServer

// Agregar servicios de sesión
builder.Services.AddDistributedMemoryCache();  // Utiliza memoria para almacenar las sesiones
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);  // Definir el tiempo de inactividad
    options.Cookie.HttpOnly = true;  // Seguridad: hacer que la cookie sea accesible solo por HTTP
    options.Cookie.IsEssential = true;  // Necesario para cumplir con GDPR
});

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // El valor predeterminado de HSTS es 30 días. Puedes cambiarlo en escenarios de producción.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

// Habilitar el uso de sesiones
app.UseSession();

app.UseRouting();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
