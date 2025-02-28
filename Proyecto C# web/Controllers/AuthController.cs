using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using insertarDatosApp.Models;
using System.Threading.Tasks;

public class AuthController : Controller
{
    private readonly ApplicationDbContext _context;

    public AuthController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public IActionResult Login()
    {
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> Login(LoginViewModel model)
    {
        if (!ModelState.IsValid)
        {
            ViewBag.Error = "Todos los campos son requeridos.";
            return View(model);
        }

        var usuario = await _context.Usuarios
            .FirstOrDefaultAsync(u => u.NombreUsuario == model.NombreUsuario && u.Contrasena == model.Contrasena);

        if (usuario != null)
        {
            HttpContext.Session.SetString("UsuarioId", usuario.Id.ToString());
            return RedirectToAction("Dashboard", "Auth");
        }

        ViewBag.Error = "Usuario o contraseña incorrecta.";
        return View(model);
    }

    [HttpGet]
    public IActionResult Registrar()
    {
        return View();
    }
    
  
    [HttpPost]
    public IActionResult Logout()
    {
        HttpContext.Session.Remove("UsuarioId");
        return RedirectToAction("Login");
    }

    public IActionResult Dashboard()
    {
        return View();
    }

    public IActionResult Crud()
    {
        var usuarios = _context.Usuarios.ToList();
        return PartialView("Crud", usuarios);
    }

  
    [HttpGet]
    public IActionResult Agregar()
    {
        return PartialView("Agregar", new Usuario());
    }

    [HttpPost]
    public async Task<IActionResult> Agregar(Usuario usuario)
    {
        if (!ModelState.IsValid)
        {
            return PartialView("Agregar", usuario);
        }

        _context.Usuarios.Add(usuario);
        await _context.SaveChangesAsync();

        TempData["MensajeExito"] = "Usuario agregado exitosamente.";
        return RedirectToAction(nameof(Dashboard));
    }

    [HttpGet]
    public async Task<IActionResult> Editar(int id)
    {
        var usuario = await _context.Usuarios.FindAsync(id);
        if (usuario == null)
        {
            return NotFound();
        }

        return PartialView("Editar", usuario);
    }

    [HttpPost]
    public async Task<IActionResult> Editar(Usuario usuario)


    
    {
        if (!ModelState.IsValid)
        {
            return PartialView("Editar", usuario);
        }

        var usuarioExistente = await _context.Usuarios.FindAsync(usuario.Id);
        if (usuarioExistente == null)
        {
            return NotFound();
        }

        usuarioExistente.NombreUsuario = usuario.NombreUsuario;
        usuarioExistente.Contrasena = usuario.Contrasena;
        usuarioExistente.Email = usuario.Email;
        usuarioExistente.Telefono = usuario.Telefono;

        await _context.SaveChangesAsync();

        TempData["MensajeExito"] = "El usuario fue actualizado exitosamente.";
        return RedirectToAction(nameof(Dashboard));
    }


      [HttpPost]
    public async Task<IActionResult> Eliminar(int id)
    {
        var usuario = await _context.Usuarios.FindAsync(id);
        if (usuario == null)
        {
            return NotFound();
        }

        _context.Usuarios.Remove(usuario);
        await _context.SaveChangesAsync();

        TempData["MensajeExito"] = "El contacto fue eliminado exitosamente.";
        return RedirectToAction(nameof(Dashboard));
    }

public IActionResult Productos()
{
    // Devolver la vista parcial sin layout
    return PartialView("/Views/Auth/Productos.cshtml"); // Especifica la ruta exacta si es necesario
}


public IActionResult inicio()
{
    // Devolver la vista parcial sin layout
    return PartialView("/Views/Auth/Dashboard.cshtml"); // Especifica la ruta exacta si es necesario
}


}
