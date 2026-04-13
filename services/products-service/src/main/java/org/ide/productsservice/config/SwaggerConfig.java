package org.ide.productsservice.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .components(new Components()
                        .addSecuritySchemes("Bearer Authentication",
                                new SecurityScheme()
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Ingresa tu token JWT. Los endpoints que requieren autenticación esperan: Authorization: Bearer <tu_token>")))
                .info(new Info()
                        .title("Products Service API")
                        .version("1.0.0")
                        .description("""
                                Microservicio para la gestión de productos y categorías en una plataforma e-commerce.
                                
                                🔐 SEGURIDAD:
                                - GET endpoints: Sin autenticación (lectura pública)
                                - POST/PUT/DELETE endpoints: Requieren JWT token
                                
                                📝 CÓMO USAR:
                                1. Obtén un token JWT de tu microservicio de usuarios (FastAPI Python)
                                2. En Swagger, usa el botón "Authorize" en la esquina superior derecha
                                3. Ingresa: Bearer <tu_token>
                                4. Ahora puedes usar endpoints protegidos
                                
                                ❌ ERRORES COMUNES:
                                - 401 Unauthorized: Token falta o es inválido
                                - 403 Forbidden: Token no tiene permisos suficientes
                                """)
                        .contact(new Contact()
                                .name("API Support")
                                .email("support@ecommerce.com")));
    }
}

