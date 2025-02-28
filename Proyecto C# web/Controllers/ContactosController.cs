using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;

public class ContactosController : Controller
{
    private readonly ApplicationDbContext _context;

    public ContactosController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public IActionResult Crear()
    {
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> Crear(Contacto contacto)
    {
        if (ModelState.IsValid)
        {
            _context.Add(contacto);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }
        return View(contacto);
    }

    public async Task<IActionResult> Index()
    {
        return View(await _context.Contactos.ToArrayAsync());
    }

    [HttpGet]
    public async Task<IActionResult> Editar(int id)
    {
        var contacto = await _context.Contactos.FindAsync(id);
        if (contacto == null)
        {
            return NotFound();
        }
        return View(contacto);
    }

    [HttpPost]
    public async Task<IActionResult> Editar(int id, Contacto contacto)
    {
        if (id != contacto.Id)
        {
            return BadRequest();
        }

        if (ModelState.IsValid)
        {
            _context.Update(contacto);
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        return View(contacto);
    }

    [HttpPost]
    public async Task<IActionResult> Eliminar(int id)
    {
        var contacto = await _context.Contactos.FindAsync(id);
        if (contacto == null)
        {
            return NotFound();
        }

        _context.Contactos.Remove(contacto);
        await _context.SaveChangesAsync();

        TempData["MensajeExito"] = "El contacto fue eliminado exitosamente.";
        return RedirectToAction(nameof(Index));
    }
}
