

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session, func, select

from app.model.product import Product
from app.schema import CreateProduct, ProductDto, ProductResponse, UpdateProduct


def create_product(
    product: CreateProduct,
    session: Session
) -> ProductResponse:

    existing_product = session.exec(
        select(Product).where(Product.name == product.name)
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail=f"Product with name '{product.name}' already exists."
        )

    db_product = Product(
        name=product.name,
        description=product.description,
        cost=product.cost,
        pictures=product.pictures
    )

    session.add(db_product)

    session.commit()

    session.refresh(db_product)

    return ProductResponse(
        message="Product created successfully.",
        product=ProductDto.model_validate(db_product)
    )


def get_product_by_id(
    product_id: int,
    session: Session
) -> ProductDto:

    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found."
        )

    return ProductDto.model_validate(product)


def get_products(session: Session) -> list[ProductDto]:
    products = session.exec(select(Product)).all()

    return [
        ProductDto.model_validate(product)
        for product in products
    ]

def update_product(
    product_id: int,
    updated_product: UpdateProduct,
    session: Session,
) -> ProductResponse:

    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found.",
        )

    update_data = updated_product.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(product, field, value)

    product.updated_at = datetime.now(timezone.utc)

    session.add(product)

    session.commit()

    session.refresh(product)

    return ProductResponse(
        message="Product updated successfully.",
        product=ProductDto.model_validate(product),
    )


def delete_product(
    product_id: int,
    session: Session,
) -> dict:

    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found."
        )

    session.delete(product)

    session.commit()

    return {
        "message": "Product deleted successfully."
    }