package org.ide.productsservice.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.ide.productsservice.dto.CategoriaDTO;
import org.ide.productsservice.service.CategoriaService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;

import java.util.List;

@RestController
@RequestMapping("/api/categories")
@RequiredArgsConstructor
@Tag(name = "Categorías", description = "API para gestionar categorías de productos")
public class CategoriaController {

    private final CategoriaService categoriaService;

    @GetMapping
    @Operation(summary = "Obtener todas las categorías",
            description = "Endpoint público - No requiere autenticación")
    public ResponseEntity<List<CategoriaDTO>> obtenerTodas() {
        List<CategoriaDTO> categorias = categoriaService.obtenerTodas();
        return ResponseEntity.ok(categorias);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Obtener categoría por ID",
            description = "Endpoint público - No requiere autenticación")
    public ResponseEntity<CategoriaDTO> obtenerPorId(@PathVariable Long id) {
        CategoriaDTO categoria = categoriaService.obtenerPorId(id);
        return ResponseEntity.ok(categoria);
    }

    @PostMapping
    @SecurityRequirement(name = "Bearer Authentication")
    @Operation(summary = "Crear nueva categoría",
            description = "Requiere token JWT en header: Authorization: Bearer <token>")
    public ResponseEntity<CategoriaDTO> crear(@Valid @RequestBody CategoriaDTO categoriaDTO) {
        CategoriaDTO categoriaNueva = categoriaService.crear(categoriaDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(categoriaNueva);
    }

    @PutMapping("/{id}")
    @SecurityRequirement(name = "Bearer Authentication")
    @Operation(summary = "Actualizar categoría",
            description = "Requiere token JWT en header: Authorization: Bearer <token>")
    public ResponseEntity<CategoriaDTO> actualizar(
            @PathVariable Long id,
            @Valid @RequestBody CategoriaDTO categoriaDTO) {
        CategoriaDTO categoriaActualizada = categoriaService.actualizar(id, categoriaDTO);
        return ResponseEntity.ok(categoriaActualizada);
    }

    @DeleteMapping("/{id}")
    @SecurityRequirement(name = "Bearer Authentication")
    @Operation(summary = "Eliminar categoría",
            description = "Requiere token JWT en header: Authorization: Bearer <token>")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        categoriaService.eliminar(id);
        return ResponseEntity.noContent().build();
    }
}

