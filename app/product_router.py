from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.schema import (
    CreateProduct,
    UpdateProduct,
    ProductResponse,
    ProductDto,
)
from app.services.product_service import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product,
)
from app.session import get_session

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
)
def create_product_endpoint(
    product: CreateProduct,
    session: Session = Depends(get_session),
):
    return create_product(product, session)


@router.get(
    "/",
    response_model=list[ProductDto],
)
def get_all_products(
    session: Session = Depends(get_session),
):
    return get_products(session)

@router.get(
    "/{product_id}",
    response_model=ProductDto,
)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    return get_product_by_id(
        product_id,
        session,
    )


@router.get(
    "/{product_id}",
    response_model=ProductDto,
)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    return get_product_by_id(
        product_id,
        session,
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product_endpoint(
    product_id: int,
    product: UpdateProduct,
    session: Session = Depends(get_session),
):
    return update_product(
        product_id,
        product,
        session,
    )


@router.delete(
    "/{product_id}",
)
def delete_product_endpoint(
    product_id: int,
    session: Session = Depends(get_session),
):
    return delete_product(
        product_id,
        session,
    )