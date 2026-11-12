from measured_rag.domain.entities import Chunk, Document, SourceProvenance


def test_domain_entities_preserve_original_and_enriched_text() -> None:
    prov = SourceProvenance(
        source_url="https://example.org/doc",
        title="Example",
        publication_date="2024-01-01",
        version="1",
        license_or_terms="CC BY 4.0",
    )
    doc = Document(id="d1", content="content", provenance=prov)
    chunk = Chunk(id="c1", document_id=doc.id, text="original text", enriched_text="context: original text")
    assert chunk.text == "original text"
    assert chunk.enriched_text is not None
    assert doc.provenance is not None
    assert doc.provenance.source_url.startswith("https://")
