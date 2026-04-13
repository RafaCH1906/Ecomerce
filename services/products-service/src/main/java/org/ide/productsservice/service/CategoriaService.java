package org.ide.productsservice.service;

import org.ide.productsservice.dto.CategoriaDTO;
import org.ide.productsservice.exception.ResourceNotFoundException;
import org.ide.productsservice.model.Categoria;
import org.ide.productsservice.repository.CategoriaRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional
public class CategoriaService {

    private final CategoriaRepository categoriaRepository;

    public List<CategoriaDTO> obtenerTodas() {
        return categoriaRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public CategoriaDTO obtenerPorId(Long id) {
        Categoria categoria = categoriaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con ID: " + id));
        return convertToDTO(categoria);
    }

    public CategoriaDTO crear(CategoriaDTO categoriaDTO) {
        Categoria categoria = Categoria.builder()
                .nombre(categoriaDTO.getNombre())
                .descripcion(categoriaDTO.getDescripcion())
                .build();
        Categoria categoriaGuardada = categoriaRepository.save(categoria);
        return convertToDTO(categoriaGuardada);
    }

    public CategoriaDTO actualizar(Long id, CategoriaDTO categoriaDTO) {
        Categoria categoria = categoriaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con ID: " + id));

        if (categoriaDTO.getNombre() != null) {
            categoria.setNombre(categoriaDTO.getNombre());
        }
        if (categoriaDTO.getDescripcion() != null) {
            categoria.setDescripcion(categoriaDTO.getDescripcion());
        }

        Categoria categoriaActualizada = categoriaRepository.save(categoria);
        return convertToDTO(categoriaActualizada);
    }

    public void eliminar(Long id) {
        Categoria categoria = categoriaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con ID: " + id));
        categoriaRepository.delete(categoria);
    }

    private CategoriaDTO convertToDTO(Categoria categoria) {
        return CategoriaDTO.builder()
                .id(categoria.getId())
                .nombre(categoria.getNombre())
                .descripcion(categoria.getDescripcion())
                .build();
    }
}

