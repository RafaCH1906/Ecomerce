package org.ide.productsservice.repository;

import org.ide.productsservice.model.Producto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductoRepository extends JpaRepository<Producto, Long> {

    @Query("SELECT p FROM Producto p WHERE p.activo = true ORDER BY p.id DESC")
    Page<Producto> findAll(Pageable pageable);

    @Query("SELECT p FROM Producto p WHERE p.categoria.id = :categoriaId AND p.activo = true ORDER BY p.id DESC")
    Page<Producto> findByCategoria_Id(Long categoriaId, Pageable pageable);
}

