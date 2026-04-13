package org.ide.productsservice.service;

import org.ide.productsservice.dto.ProductoDTO;
import org.ide.productsservice.exception.ResourceNotFoundException;
import org.ide.productsservice.model.Categoria;
import org.ide.productsservice.model.Producto;
import org.ide.productsservice.repository.CategoriaRepository;
import org.ide.productsservice.repository.ProductoRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
@Transactional
public class ProductoService {

    private final ProductoRepository productoRepository;
    private final CategoriaRepository categoriaRepository;

    public Page<ProductoDTO> obtenerTodos(Pageable pageable) {
        return productoRepository.findAll(pageable)
                .map(this::convertToDTO);
    }

    public ProductoDTO obtenerPorId(Long id) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Producto no encontrado con ID: " + id));
        return convertToDTO(producto);
    }

    public Page<ProductoDTO> obtenerPorCategoria(Long categoriaId, Pageable pageable) {
        // Verificar que la categoría existe
        categoriaRepository.findById(categoriaId)
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con ID: " + categoriaId));

        return productoRepository.findByCategoria_Id(categoriaId, pageable)
                .map(this::convertToDTO);
    }

    public ProductoDTO crear(ProductoDTO productoDTO) {
        Categoria categoria = categoriaRepository.findById(productoDTO.getCategoriaId())
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con ID: " + productoDTO.getCategoriaId()));

        Producto producto = Producto.builder()
                .nombre(productoDTO.getNombre())
                .descripcion(productoDTO.getDescripcion())
                .precio(productoDTO.getPrecio())
                .stock(productoDTO.getStock())
                .activo(true)
                .categoria(categoria)
                .build();

        Producto productoGuardado = productoRepository.save(producto);
        return convertToDTO(productoGuardado);
    }

    public ProductoDTO actualizar(Long id, ProductoDTO productoDTO) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Producto no encontrado con ID: " + id));

        if (productoDTO.getNombre() != null) {
            producto.setNombre(productoDTO.getNombre());
        }
        if (productoDTO.getDescripcion() != null) {
            producto.setDescripcion(productoDTO.getDescripcion());
        }
        if (productoDTO.getPrecio() != null) {
            producto.setPrecio(productoDTO.getPrecio());
        }
        if (productoDTO.getStock() != null) {
            producto.setStock(productoDTO.getStock());
        }
        if (productoDTO.getActivo() != null) {
            producto.setActivo(productoDTO.getActivo());
        }
        if (productoDTO.getCategoriaId() != null) {
            Categoria categoria = categoriaRepository.findById(productoDTO.getCategoriaId())
                    .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con ID: " + productoDTO.getCategoriaId()));
            producto.setCategoria(categoria);
        }

        Producto productoActualizado = productoRepository.save(producto);
        return convertToDTO(productoActualizado);
    }

    public void eliminar(Long id) {
        Producto producto = productoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Producto no encontrado con ID: " + id));
        // Soft delete: marcar como inactivo en lugar de eliminar
        producto.setActivo(false);
        productoRepository.save(producto);
    }

    private ProductoDTO convertToDTO(Producto producto) {
        return ProductoDTO.builder()
                .id(producto.getId())
                .nombre(producto.getNombre())
                .descripcion(producto.getDescripcion())
                .precio(producto.getPrecio())
                .stock(producto.getStock())
                .activo(producto.getActivo())
                .categoriaId(producto.getCategoria().getId())
                .build();
    }
}

